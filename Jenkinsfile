pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 10, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }

    stages {
        stage('Build') {
            steps {
                echo '=== BUILD: เตรียมสภาพแวดล้อมและตรวจ syntax ==='
                script {
                    if (isUnix()) {
                        sh '''
                            python3 --version
                            python3 -m venv .venv
                            .venv/bin/python -m pip install --quiet -r requirements.txt
                            .venv/bin/python -m py_compile todo.py storage.py app.py server.py
                        '''
                    } else {
                        bat '''
                            @echo off
                            python --version
                            python -m venv .venv
                            .venv\\Scripts\\python.exe -m pip install --quiet -r requirements.txt
                            .venv\\Scripts\\python.exe -m py_compile todo.py storage.py app.py server.py
                        '''
                    }
                }
            }
        }

        stage('Test') {
            steps {
                echo '=== TEST: รัน unit test + API test ==='
                script {
                    if (isUnix()) {
                        sh '.venv/bin/python -m pytest -v --junitxml=test-results.xml'
                    } else {
                        bat '.venv\\Scripts\\python.exe -m pytest -v --junitxml=test-results.xml'
                    }
                }
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }

        stage('Deploy') {
            steps {
                echo '=== DEPLOY: เตรียมไฟล์และ smoke test ใน temporary directory ==='
                script {
                    if (isUnix()) {
                        sh '.venv/bin/python scripts/deploy_smoke.py'
                    } else {
                        bat '.venv\\Scripts\\python.exe scripts\\deploy_smoke.py'
                    }
                }
                archiveArtifacts artifacts: 'todo-app.tar.gz', fingerprint: true
            }
        }
    }

    post {
        success { echo 'Pipeline สำเร็จ: Build, Test, Deploy ผ่านทั้งหมด' }
        failure { echo 'Pipeline ล้มเหลว: ดู Console Output เพื่อตรวจสอบ' }
        always {
            script {
                if (isUnix()) {
                    sh 'rm -rf .venv'
                } else {
                    bat 'if exist .venv rmdir /s /q .venv'
                }
            }
        }
    }
}
