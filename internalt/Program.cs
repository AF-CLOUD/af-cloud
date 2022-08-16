using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.Playwright;
using System.Net.Http;
using System.Net;
using System.Security.Cryptography;
using System.Text;



namespace internalt
{
    internal class MainClass
    {

        static string LoginUrl = "https://accounts.google.com/ServiceLogin/signinchooser?service=wise&passive=true&continue=http%3A%2F%2Fdrive.google.com%2F%3Futm_source%3Den&utm_medium=button&utm_campaign=web&utm_content=gotodrive&usp=gtd&ltmpl=drive&flowName=GlifWebSignIn&flowEntry=ServiceLogin";
        static string placeholderforUserId = "input[type=\"email\"]";
        static string placeholderforpwd = "input[type=\"password\"]";
        static string userid = "af.cloud.2021@gmail.com";
        static string password = "dfrc4738!@#";
        static Dictionary<string,string> essential_cookie = new Dictionary<string,string>();

        static CookieContainer cook = new CookieContainer();


        /*
        public OnedriveManager(string userid, string password) 
        {
        Userid = userid;
        Password = password;
        }


        public string Userid { get; set; }
        public string Password { get; set; }
        */




        public void Login(string userid, string password)
        {


            Task.Run(async () =>
            {
                await LoginAsync();
            }).Wait();


        }

        internal static async Task LoginAsync()
        {


            try
            {
                var exitCode = Microsoft.Playwright.Program.Main(new[] { "install" });
                if (exitCode != 0)
                {
                    Console.WriteLine("Browsers not installed");
                }


                Console.WriteLine("Browsers installed");


                // Launch browser
                var playwright = await Playwright.CreateAsync();
                var browser = await playwright.Firefox.LaunchAsync(new BrowserTypeLaunchOptions { Headless = false });


                // Connect to the OneDrive url
                var page = await browser.NewPageAsync();
                await page.GotoAsync(LoginUrl);


                // Input UserID
                var frameforuserid = page.Locator(placeholderforUserId);
                await frameforuserid.FillAsync(userid);


                var framefornextbtn = page.Locator("#identifierNext");
                await framefornextbtn.ClickAsync();


                // Input UserPWD
                var frameforpwd = page.Locator(placeholderforpwd);
                await frameforpwd.FillAsync(password);


                var frameforloginbtn = page.Locator("#passwordNext");
                await frameforloginbtn.ClickAsync();


                // Wait for the browser to reload
                await page.WaitForTimeoutAsync(3000);


                

                var all_cookies = await page.Context.CookiesAsync();

                foreach(var cookie in all_cookies)
                {

                    essential_cookie[cookie.Name] = cookie.Value;
                    
                }


                // SAPISIDHASH 계산
                string s = essential_cookie["SAPISID"] + " " + "https://drive.google.com";
                byte[] b = Encoding.UTF8.GetBytes(s); 
                SHA1 sha1 = new SHA1CryptoServiceProvider();
                var a = sha1.ComputeHash(b);
                string sapisid = Convert.ToHexString(a);


                essential_cookie["SAPISIDHASH"] = sapisid;



                var handler = new HttpClientHandler();

                handler.ServerCertificateCustomValidationCallback = (requestMessage, certificate, chain, policyErrors) => true;


                // In production code, don't destroy the HttpClient through using, but better use IHttpClientFactory factory or at least reuse an existing HttpClient instance
                // https://docs.microsoft.com/en-us/aspnet/core/fundamentals/http-requests
                // https://www.aspnetmonsters.com/2016/08/2016-08-27-httpclientwrong/
                using (var httpClient = new HttpClient(handler))
                {
                    using (var request = new HttpRequestMessage(new HttpMethod("GET"), "https://clients6.google.com/batch/drive/v2internal/files?openDrive=false&reason=305&syncType=0&errorRecovery=false&q&incompleteSearch&appDataFilter=NO_APP_DATA&maxResults=22000&supportsTeamDrives=true&includeItemsFromAllDrives=true&corpora=default&retryCount=0&key=AIzaSyAy9VVXHSpS2IJpptzYtGbLP3-3_l0aBk4"))
                    {
                        request.Headers.TryAddWithoutValidation("Host", "clients6.google.com");
                        request.Headers.TryAddWithoutValidation("Connection", "keep-alive");
                        request.Headers.TryAddWithoutValidation("sec-ch-ua", "\"Chromium\";v=\"104\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"104\"");
                        request.Headers.TryAddWithoutValidation("sec-ch-ua-mobile", "?0");
                        request.Headers.TryAddWithoutValidation("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36");
                        request.Headers.TryAddWithoutValidation("sec-ch-ua-platform", "\"Windows\"");
                        request.Headers.TryAddWithoutValidation("authorization", "SAPISIDHASH " + essential_cookie["SAPISIDHASH"]);
                        request.Headers.TryAddWithoutValidation("Accept", "*/*");
                        request.Headers.TryAddWithoutValidation("Origin", "https://drive.google.com");
                        request.Headers.TryAddWithoutValidation("X-Client-Data", "CIu2yQEIorbJAQjBtskBCKmdygEIoNPKAQiG/8oBCJKhywEIi6vMAQiKvMwBCO+8zAEI3MDMAQiawcwBCLPBzAEIxcHMAQjXwcwBCNjEzAEIvcbMAQidycwBCOLLzAEYranKAQ==");
                        request.Headers.TryAddWithoutValidation("Sec-Fetch-Site", "same-site");
                        request.Headers.TryAddWithoutValidation("Sec-Fetch-Mode", "cors");
                        request.Headers.TryAddWithoutValidation("Sec-Fetch-Dest", "empty");
                        request.Headers.TryAddWithoutValidation("Referer", "https://drive.google.com/");
                        request.Headers.TryAddWithoutValidation("Accept-Language", "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7");
                        request.Headers.TryAddWithoutValidation("Cookie", "SID=" + essential_cookie["SID"]);
                        request.Headers.TryAddWithoutValidation("Cookie", "HSID=" + essential_cookie["HSID"]);
                        request.Headers.TryAddWithoutValidation("Cookie", "SSID=" + essential_cookie["SSID"]);
                        request.Headers.TryAddWithoutValidation("Cookie", "APISID=" + essential_cookie["APISID"]);
                        request.Headers.TryAddWithoutValidation("Cookie", "SAPISID=" + essential_cookie["SAPISID"]);

                        var response = await httpClient.SendAsync(request);
                        Console.WriteLine(response.Content.ReadAsStringAsync().Result);

                    }


                }

            }




            catch (Exception e)
            {
                Console.WriteLine("Login Error");


            }

        }
    


static async Task Main(string[] args)
        {
            var m = new MainClass();

            m.Login(userid, password);

            Console.WriteLine(essential_cookie["SAPISIDHASH"]);
        }

    }
}