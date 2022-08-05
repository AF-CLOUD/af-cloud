// Copyright 2022 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// [START drive_list_appdata]
using Google.Apis.Auth.OAuth2;
using Google.Apis.Drive.v3;
using Google.Apis.Drive.v3.Data;
using Google.Apis.Services;
using System;
using System.Net;
using System.IO;


namespace DriveV3Snippets
{
    // Class to demonstrate use-case of Drive's list files in the application data folder.
    public class ListAppData
    {
        /// <summary>
        /// List down files in the application data folder.
        /// </summary>
        /// <returns>list of 10 files, null otherwise.</returns>
        public static IList<Google.Apis.Drive.v3.Data.File> DriveListAppData(DriveService service ,UserCredential credential)
        {
            try
            {
                /* Load pre-authorized user credentials from the environment.
                 TODO(developer) - See https://developers.google.com/identity for
                 guides on implementing OAuth2 for your application. */



                FilesResource.ListRequest listRequest = service.Files.List();
                listRequest.PageSize = 100;
                listRequest.Fields = "nextPageToken, files(id, name, mimeType, size, trashed, modifiedTime), files(createdTime, thumbnailLink, hasThumbnail, shared)";


                IList<Google.Apis.Drive.v3.Data.File> files = listRequest.Execute().Files;
                Console.WriteLine("Files:");
                if (files == null || files.Count == 0)
                {
                    Console.WriteLine("No files found.");
                    return null;
                }

                int i = 0;

                foreach (var file in files)
                {
                    Console.WriteLine("{0} {1} {2} {3} {4} {5} {6} ({7}) {8}", i, file.Name, file.Id, file.MimeType, file.Size, file.Trashed, file.ModifiedTime, file.ThumbnailLink, file.CreatedTime);
                    i = i + 1;

                    
                    
                    if (file.ThumbnailLink != null)
                    {

                        string t_name = Path.GetFileNameWithoutExtension(file.Name);
                        using (var mywebClient = new WebClient())
                        {
                            bool y = file.ThumbnailLink.Contains("lh");

                            if (y == false)
                            {
                                string a = file.ThumbnailLink + "&access_token=" + credential.Token.AccessToken;
                                mywebClient.Headers.Add("user-agent", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.0.3705;)");
                                mywebClient.DownloadFile(a, "c:/files/thumbnail/" + t_name + ".png");
                            }
                            else
                            {
                                string a = file.ThumbnailLink;
                                mywebClient.Headers.Add("user-agent", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.0.3705;)");
                                mywebClient.DownloadFile(a, "c:/files/thumbnail/" + t_name + ".png");
                            }




                        }

                    }
                    
                    

                    /*
                    if (file.ThumbnailLink != null) {
                    string t_name = Path.GetFileNameWithoutExtension(file.Name);
                    string a = file.ThumbnailLink.ToString();
                    DownloadRemoteImageFile(a, "c:/files/thumbnail/" + t_name + ".png");
                    }
                    */
                }
                /*
                string l = "https://lh6.googleusercontent.com/FtZGmJldiv1rY75Poed6SD2P6yJOq9uZUrcFyPcA-veB2du9oTh7aPwfLbgtTNtoRjTMVuQFjszuEWw=s220";
                string name = "wallpaperbetter (2)";
                using (var mywebClient = new WebClient())
                {

                    mywebClient.Headers.Add("user-agent", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.0.3705;)");
                    mywebClient.DownloadFile(l, "c:/files/thumbnail/" +name + ".png"); ;

                }


                */


                return files;

            }
            catch (Exception e)
            {
                // TODO(developer) - handle error appropriately
                if (e is AggregateException)
                {
                    Console.WriteLine("Credential Not found");
                }
                else
                {
                    throw;
                }
            }
            return null;
        }

        static bool DownloadRemoteImageFile(string uri, string fileName)
        {
            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(uri);
            HttpWebResponse response = (HttpWebResponse)request.GetResponse();
            bool bImage = response.ContentType.StartsWith("image",
                StringComparison.OrdinalIgnoreCase);
            if ((response.StatusCode == HttpStatusCode.OK ||
                response.StatusCode == HttpStatusCode.Moved ||
                response.StatusCode == HttpStatusCode.Redirect) &&
                bImage)
            {
                using (Stream inputStream = response.GetResponseStream())
                using (Stream outputStream = System.IO.File.OpenWrite(fileName))
                {
                    byte[] buffer = new byte[4096];
                    int bytesRead;
                    do
                    {
                        bytesRead = inputStream.Read(buffer, 0, buffer.Length);
                        outputStream.Write(buffer, 0, bytesRead);
                    } while (bytesRead != 0);
                }

                return true;
            }
            else
            {
                return false;
            }
        }
    }
}
// [END drive_list_appdata]