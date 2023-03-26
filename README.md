# Introduction 
TODO: Give a short introduction of your project. Let this section explain the objectives or the motivation behind this project. 

# Getting Started
TODO: Guide users through getting your code up and running on their own system. In this section you can talk about:
1.	Installation process
        Step 1:Goto root folder and execute the below command from terminal 
               pip install -r requirements.txt
        Step 2: One the above command is executed, execute below command from same terminal
               playwright install
2.	Software dependencies
3.	Latest releases
4.	API references


# Contribute
TODO: Explain how other users and developers can contribute to make your code better. 

If you want to learn more about creating good readme files then refer the following [guidelines](https://docs.microsoft.com/en-us/azure/devops/repos/git/create-a-readme?view=azure-devops). You can also seek inspiration from the below readme files:
- [ASP.NET Core](https://github.com/aspnet/Home)
- [Visual Studio Code](https://github.com/Microsoft/vscode)
- [Chakra Core](https://github.com/Microsoft/ChakraCore)

# Build and Test
TODO: Describe and show how to build your code and run the tests. 
To run specific spec in sequential open Terminal and give the following command

    gauge run --env="default" .\test_suite\features\specs\login.spec

To run all specs in sequential open Terminal and give the following command

    gauge run --env="default" .\test_suite\features\specs\

To run all parallel -open Terminal and give the following command

    gauge run --parallel -n=4 --env="default" .\test_suite\features\specs\

Rerun failed test case -open Terminal and give the following command

    gauge run --failed

Rerun failed scenarios by max-retries-count -open Terminal and give the following command

    gauge run --max-retries-count=4

Rerun failed scenarios by max-retries-count and retry-only -open Terminal and give the following command

    gauge run --max-retries-count=3 --retry-only="should-retry"

To generate flash report open browser and paste the url

    Add port number in default env file (FLASH_SERVER_PORT=1443)
    Flash report Url - http://127.0.0.1:1443/