// See https://aka.ms/new-console-template for more information
//Console.WriteLine("Hello, World!");

using DriveV3Snippets;
using Google.Apis.Auth.OAuth2;
using Google.Apis.Drive.v3;
using Google.Apis.Services;
using Google.Apis.Util.Store;

namespace DriveV3Example
{
    internal class MainClass
    {
        static protected DriveService service;
        static string[] Scopes = {DriveService.Scope.DriveReadonly};
        private string filePath = "files/photo.jpg";
        static string ApplicationName = "Drive API .NET Quickstart";


        public void TestDownloadFile()
        {
            var id = CreateTestBlob(filePath);
            var fileStream = DownloadFile.DriveDownloadFile(id, service);
            DeleteFileOnCleanup(id);
        }

        static void Main(string[] args)
        {
            Console.WriteLine("Hello");
            MainClass m = new MainClass();
            UserCredential credential = null;

            // 크리덴셜 인증
            try
            {

                // Load client secrets.
                using (var stream =
                       new FileStream("credentials.json", FileMode.Open, FileAccess.Read))
                {
                    /* The file token.json stores the user's access and refresh tokens, and is created
                     automatically when the authorization flow completes for the first time. */
                    string credPath = "token.json";
                    credential = GoogleWebAuthorizationBroker.AuthorizeAsync(
                        GoogleClientSecrets.FromStream(stream).Secrets,
                        Scopes,
                        "user",
                        CancellationToken.None,
                        new FileDataStore(credPath, true)).Result;
                    Console.WriteLine("Credential file saved to: " + credPath);
                }

                // Create Drive API service.
                service = new DriveService(new BaseClientService.Initializer
                {
                    HttpClientInitializer = credential,
                    ApplicationName = ApplicationName
                });
            }
            


            catch (FileNotFoundException e)
            {
                Console.WriteLine(e.Message);
            }

            Console.WriteLine(credential.Token.AccessToken);


            // 파일 리스트 획득
            IList<Google.Apis.Drive.v3.Data.File> files = ListAppData.DriveListAppData(service ,credential);


            

            // 파일 다운로드
            Console.Write("다운 번호");
            string st = Console.ReadLine();
            int num = Convert.ToInt32(st);


            string id = files[num].Id;
            var streams = DownloadFile.DriveDownloadFile(id, service);
            Stream s = new FileStream("c:/files/" + files[num].Name, FileMode.OpenOrCreate);
            using (BinaryWriter wr = new BinaryWriter(s))
            {
                wr.Write(streams.ToArray());
            }


            //파일 검색
            SearchFiles.DriveSearchFiles(service);


            


            //m.TestDownloadFile();
        }




        public DriveService BuildService()
        {
            /* Load pre-authorized user credentials from the environment.
             TODO(developer) - See https://developers.google.com/identity for
             guides on implementing OAuth2 for your application. */
            GoogleCredential credential = GoogleCredential.GetApplicationDefault();
            var scopes = new[]
            {
                DriveService.Scope.Drive,
                DriveService.Scope.DriveAppdata
            };
            credential = credential.CreateScoped(scopes);

            // Create Drive API service.
            var service = new DriveService(new BaseClientService.Initializer
            {
                HttpClientInitializer = credential,
                ApplicationName = "Drive API Snippets"
            });

            return service;
        }

        public void Setup()
        {
            service = BuildService();
        }

        protected void DeleteFileOnCleanup(string id)
        {
            if (service != null){
                service.Files.Delete(id).Execute();
            }

         }

        protected string CreateTestDocument(string filePath)
        {
            var fileMetadata = new Google.Apis.Drive.v3.Data.File();
            fileMetadata.Name = "Test Document";
            fileMetadata.MimeType = "application/vnd.google-apps.document";
            using (var stream = new FileStream(filePath,
                       FileMode.Open))
            {
                var request = service.Files.Create(
                    fileMetadata, stream, "text/plain");
                request.Fields = "id, mimeType";
                request.Upload();
                var file = request.ResponseBody;
                if (file != null)
                {
                    return file.Id;
                }
                else
                {
                    return null;
                }
            }
        }


        protected string CreateTestBlob(string filePath)
        {
            var fileMetadata = new Google.Apis.Drive.v3.Data.File();
            fileMetadata.Name = "photo.jpg";
            using (var stream = new FileStream(filePath, FileMode.Open))
            {
                if (service != null)
                {
                    var request = service.Files.Create(
                        fileMetadata, stream, "image/jpeg");
                    request.Fields = "id";
                    request.Upload();
                    var file = request.ResponseBody;
                    return file.Id;
                }

                else
                {

                    Console.WriteLine("NO service");
                    return "0";
                }


            }
        }
    }
}
