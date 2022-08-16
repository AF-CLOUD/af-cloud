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

// [START drive_export_pdf]
using Google.Apis.Auth.OAuth2;
using Google.Apis.Download;
using Google.Apis.Drive.v3;
using Google.Apis.Services;

namespace DriveV3Snippets
{
    // Class to demonstrate use of Drive export pdf
    public class ExportPdf
    {
        /// <summary>
        /// Download a Document file in PDF format.
        /// </summary>
        /// <param name="fileId">Id of the file.</param>
        /// <returns>Byte array stream if successful, null otherwise</returns>
        public static MemoryStream DriveExportPdf(Google.Apis.Drive.v3.Data.File files, DriveService service)
        {
            try
            {



                Dictionary<string, string> dic_type = new Dictionary<string, string>();
                Dictionary<string, string> ext_type = new Dictionary<string, string>();

                dic_type.Add("application/vnd.google-apps.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.document");
                dic_type.Add("application/vnd.google-apps.spreadsheet", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet");
                dic_type.Add("application/vnd.google-apps.presentation", "application/vnd.openxmlformats-officedocument.presentationml.presentation");


                ext_type.Add("application/vnd.openxmlformats-officedocument.wordprocessingml.document", ".docx");
                ext_type.Add("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", ".xlsx");
                ext_type.Add("application/vnd.openxmlformats-officedocument.presentationml.presentation", ".pptx");


                string last_type = ext_type[dic_type[files.MimeType]];

                var request = service.Files.Export(files.Id, dic_type[files.MimeType]);
                var stream = new MemoryStream();
                // Add a handler which will be notified on progress changes.
                // It will notify on each chunk download and when the
                // download is completed or failed.
                request.MediaDownloader.ProgressChanged +=
                    progress =>
                    {
                        switch (progress.Status)
                        {
                            case DownloadStatus.Downloading:
                            {
                                Console.WriteLine(progress.BytesDownloaded);
                                break;
                            }
                            case DownloadStatus.Completed:
                            {
                                Console.WriteLine("Download complete.");
                                break;
                            }
                            case DownloadStatus.Failed:
                            {
                                Console.WriteLine("Download failed.");
                                break;
                            }
                        }
                    };
                request.Download(stream);

                Stream s = new FileStream("c:/files/" + files.Name+ last_type, FileMode.OpenOrCreate);
                using (BinaryWriter wr = new BinaryWriter(s))
                {
                    wr.Write(stream.ToArray());
                }



                return null;
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
// [END drive_export_pdf]