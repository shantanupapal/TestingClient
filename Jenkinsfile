pipeline {
    agent any

    stages {
        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m pip install --upgrade pip
                    if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh 'python3 run_tests.py --test_suite regression --env staging'
            }
        }
    }

    post {
        success {
            echo "✅ Build passed"
        }
        failure {
            echo "❌ Build failed"
        }
    }
}
