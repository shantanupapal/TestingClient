pipeline {
    agent any

    environment {
        PYTHON = 'python3'
    }

    stages {
        stage('Install Dependencies') {
            steps {
                script {
                    githubNotify context: 'Build', status: 'PENDING', description: 'Installing dependencies...'
                }
                sh '''
                    ${PYTHON} -m pip install --upgrade pip
                    if [ -f requirements.txt ]; then ${PYTHON} -m pip install -r requirements.txt; fi
                '''
            }
        }

        stage('Run Default Tests') {
            steps {
                script {
                    githubNotify context: 'Build', status: 'PENDING', description: 'Running default tests...'
                    def status = sh(script: "${PYTHON} run_tests.py --test_suite regression --env staging", returnStatus: true)
                    if (status == 0) {
                        githubNotify context: 'Build', status: 'SUCCESS', description: 'Default tests passed.'
                    } else {
                        githubNotify context: 'Build', status: 'FAILURE', description: 'Default tests failed.'
                        error("Default tests failed")
                    }
                }
            }
        }

        stage('Run ATP Tests') {
            steps {
                script {
                    githubNotify context: 'ATP Tests', status: 'PENDING', description: 'Running ATP tests...'
                    def atpStatus = sh(script: "${PYTHON} atp_test_runner.py --mode full --env prod", returnStatus: true)
                    if (atpStatus == 0) {
                        githubNotify context: 'ATP Tests', status: 'SUCCESS', description: 'ATP tests passed.'
                    } else {
                        githubNotify context: 'ATP Tests', status: 'FAILURE', description: 'ATP tests failed.'
                        error("ATP tests failed")
                    }
                }
            }
        }
    }
}
