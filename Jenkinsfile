pipeline {
    agent any

    environment {
        PYTHON = 'python3'
    }

    stages {
        stage('Install Dependencies') {
            steps {
                script {
                    echo "Installing dependencies..."
                    def depStatus = sh(script: '''
                        which python3 || true
                        python3 -m pip install --upgrade pip || true
                        if [ -f requirements.txt ]; then python3 -m pip install -r requirements.txt || true; fi
                    ''', returnStatus: true)

                    if (depStatus != 0) {
                        echo "WARNING: Dependency install failed. Continuing pipeline."
                    }
                }
            }
        }

        stage('Run Default Tests') {
            steps {
                script {
                    setGitHubPullRequestStatus context: 'Build', state: 'PENDING', message: 'Running default tests...'
                    def status = sh(script: "${PYTHON} run_tests.py --test_suite regression --env staging", returnStatus: true)

                    if (status == 0) {
                        setGitHubPullRequestStatus context: 'Build', state: 'SUCCESS', message: 'Default tests passed.'
                    } else {
                        setGitHubPullRequestStatus context: 'Build', state: 'FAILURE', message: 'Default tests failed.'
                        error("Default tests failed")
                    }
                }
            }
        }

        stage('Run ATP Tests') {
            steps {
                script {
                    setGitHubPullRequestStatus context: 'ATP Tests', state: 'PENDING', message: 'Running ATP tests...'

                    def atpStatus = sh(script: "${PYTHON} atp_test_runner.py --mode full", returnStatus: true)

                    if (atpStatus == 0) {
                        setGitHubPullRequestStatus context: 'ATP Tests', state: 'SUCCESS', message: 'ATP tests passed.'
                    } else {
                        setGitHubPullRequestStatus context: 'ATP Tests', state: 'FAILURE', message: 'ATP tests failed.'
                        error("ATP tests failed")
                    }
                }
            }
        }
    }
}
