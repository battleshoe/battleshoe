*******GAEUNIT Test********
---------------------------
1.Copy the project to local system
---------------------------
2.Add the project into Google App Engine Launcher
---------------------------
3.Select the project, click run.
---------------------------
4.Wait until the project is running successfully, click browse.
---------------------------
5.Log in as battleshoe@gmail.com
---------------------------
6.Change the url "/app/main.html#/theworld" to "/coverage"
 (The reason why we didn't use "/test" is that we need to run all the test with one new clean datastore. We did try tearDown() to reset datastore for each test, but it turns out that tearDown() corrupts the data in datastore, then subsequent tests failed.)
---------------------------
8.The end.