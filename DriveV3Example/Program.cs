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
        static string[] Scopes = {DriveService.Scope.Drive};
        static string ApplicationName = "Drive API .NET Quickstart";


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
            Google.Apis.Drive.v3.Data.File f = files[num];


            bool y = f.MimeType.Contains("application/vnd.google-apps");


            if (y == true) 
            {
                 var streams = ExportPdf.DriveExportPdf(f, service);

            }
            else
            {
                var streams = DownloadFile.DriveDownloadFile(f, service);

            }




            //파일 검색
            SearchFiles.DriveSearchFiles(service);

        }



        protected void DeleteFileOnCleanup(string id)
        {
            if (service != null){
                service.Files.Delete(id).Execute();
            }

         }


       
    }
}
