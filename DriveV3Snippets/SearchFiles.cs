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

// [START drive_search_files]
using Google.Apis.Auth.OAuth2;
using Google.Apis.Drive.v3;
using Google.Apis.Services;

namespace DriveV3Snippets
{
    // Class to demonstrate use-case of Drive search files. 
    public class SearchFiles
    {   
        /// <summary>
        /// Search for specific set of files.
        /// </summary>
        /// <returns>search result list, null otherwise.</returns>
        public static IList<Google.Apis.Drive.v3.Data.File> DriveSearchFiles(DriveService service)
        {
            try
            {

                var files = new List<Google.Apis.Drive.v3.Data.File>();

                string pageToken = null;
                do
                {
                    var request = service.Files.List();


                    Console.WriteLine("0: string, 1: modifiedtime");
                    string s_num = Console.ReadLine(); 

                    if (s_num == "0")
                    {

                        Console.Write("°Ë»ö string : ");
                        string st = Console.ReadLine();

                        request.Q = "fullText contains " + "'" + st + "'";
                    
                    }

                    if (s_num == "1")
                    {

                        Console.WriteLine("start time : ex)2022-08-05");
                        string s_time = Console.ReadLine();
                        Console.WriteLine("end time : ex)2022-08-05");
                        string e_time = Console.ReadLine();

                        request.Q = "modifiedTime > '"+s_time+"' and modifiedTime < '"+e_time+"'";

                    }

                    request.Spaces = "drive";
                    request.Fields = "nextPageToken, files(id, name)";
                    request.PageToken = pageToken;
                    var result = request.Execute();
                    foreach (var file in result.Files)
                    {
                        Console.WriteLine("Found file: {0} ({1})", file.Name, file.Id);
                    }

                    // [START_EXCLUDE silent]
                    files.AddRange(result.Files);
                    // [END_EXCLUDE]
                    pageToken = result.NextPageToken;
                } while (pageToken != null);

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
    }
}
// [END drive_search_files]