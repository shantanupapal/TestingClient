pipeline {
    agent any

    stages {
        stage('Install Deps') {
            steps {
                githubNotify context: 'Build', status: 'PENDING', description: 'Installing dependencies...'
                sh '''
                    python3 -m pip install --upgrade pip
                    if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
                '''
                githubNotify context: 'Build', status: 'SUCCESS', description: 'Dependencies installed.'
            }
        }

        stage('Run Default Tests') {
            steps {
                githubNotify context: 'Build', status: 'PENDING', description: 'Running default test suite...'
                sh 'python3 run_tests.py --test_suite regression --env staging'
            }
        }

        stage('Run ATP Tests') {
            steps {
                githubNotify context: 'ATP Tests', status: 'PENDING', description: 'Running ATP tests...'
                sh 'python3 atp_test_runner.py --mode full --env prod'
            }
        }
    }

    post {
        success {
            githubNotify context: 'Build', status: 'SUCCESS', description: 'Default tests passed'
            githubNotify context: 'ATP Tests', status: 'SUCCESS', description: 'ATP tests passed'
        }
        failure {
            githubNotify context: 'Build', status: 'FAILURE', description: 'One or more tests failed'
            githubNotify context: 'ATP Tests', status: 'FAILURE', description: 'ATP test failure'
        }
    }
}
