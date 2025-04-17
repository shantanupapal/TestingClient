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
            }
        }

        stage('Run Tests') {
            steps {
                githubNotify context: 'Build', status: 'PENDING', description: 'Running tests...'
                sh 'python3 run_tests.py --test_suite regression --env staging'
            }
        }
    }

    post {
        success {
            githubNotify context: 'Build', status: 'SUCCESS', description: 'Build passed'
        }
        failure {
            githubNotify context: 'Build', status: 'FAILURE', description: 'Build failed'
        }
    }
}
