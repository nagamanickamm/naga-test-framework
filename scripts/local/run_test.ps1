Set-Variable -Name "FLASK_APP" -Value "Demo"
Set-Variable -Name "FLASK_ENV" -Value "development"

Start-Process flask -ArgumentList "--app", "neon\test\test_support\demo_api.py", "run", "--port", "5000" -Verb Open

Start-Process python -ArgumentList "-u", "neon\test\test_support\websockets_demo.py" -Verb Open

gauge run .\neon\test\functional_tests\demo\test_suite\features\specs\unit --env="azure"