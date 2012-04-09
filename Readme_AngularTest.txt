*******Angular Test********
---------------------------
0.Please use Firefox for this test. We realised that we could not do binding tests with Google Chrome. Somehow when running tests using Chrome, bindings cannot be detected. Example of our binding {{stats.money}}
---------------------------
1.Copy the project to local system
---------------------------
2.Add the project into Google App Engine Launcher
---------------------------
3.Select the project, click run.
---------------------------
4.Wait until the project is running successfully, click browse.
---------------------------
5.Log in as any user name
---------------------------
6.Change the url "/app/main.html#/theworld" to "/angulartest/e2e/runner.html".(Remain the port number unchanged and host as localhost)
---------------------------
7.IF need to run the test for multiple times, please stop the project in Google App Engine Launcher and run again after each single test.(This is to clear the datastore in order to meet the expected result in test scenario)
---------------------------
8.The end.