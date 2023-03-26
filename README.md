
Naga Test Framework
Naga Test Framework is a test automation framework built using Gauge and Selenium for web-based applications. It uses Python as the primary programming language and supports the creation and execution of tests for multiple browsers and platforms.

Tool Setup
To use Neon Test Framework, you need to have the following tools installed on your system:

Chocolatey: Chocolatey is a package manager for Windows. To install Chocolatey, open an elevated PowerShell prompt and run the following command:
less
Copy code
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
git: Git is a version control system used to manage source code. To install Git, open an elevated PowerShell prompt and run the following command:
Copy code
choco install git

Python 3.10.9: Python is a programming language used to write test automation scripts. To install Python, open an elevated PowerShell prompt and run the following command:
css
Copy code
choco install python --version=3.10.9
VSCode: VSCode is an integrated development environment (IDE) used to write and debug code. To install VSCode, download and install the latest version from https://code.visualstudio.com/download.

Gauge python: Gauge is a test automation tool used to write and execute tests. To install Gauge python, open an elevated PowerShell prompt and run the following command:

Copy code
choco install gauge-python



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
