pipeline {
    agent any

    environment {
        PYTHON = 'python3'
    }

    stages {
        stage('Install Dependencies') {
            steps {
                script {
                    try {
                        if (env.CHANGE_ID) {
                            githubNotify context: 'Build', status: 'PENDING', description: 'Installing dependencies...'
                        }
                    } catch (err) {
                        echo "WARNING: githubNotify failed for Install step: ${err.getMessage()}"
                    }

                    def depStatus = sh(script: '''
                        which python3 || true
                        python3 -m pip install --upgrade pip || true
                        if [ -f requirements.txt ]; then python3 -m pip install -r requirements.txt || true; fi
                    ''', returnStatus: true)

                    if (depStatus == 0) {
                        try {
                            if (env.CHANGE_ID) {
                                githubNotify context: 'Build', status: 'SUCCESS', description: 'Dependencies installed.'
                            }
                        } catch (err) {
                            echo "WARNING: githubNotify failed: ${err.getMessage()}"
                        }
                    } else {
                        try {
                            if (env.CHANGE_ID) {
                                githubNotify context: 'Build', status: 'FAILURE', description: 'Dependency install failed.'
                            }
                        } catch (err) {
                            echo "WARNING: githubNotify failed: ${err.getMessage()}"
                        }
                        echo "WARNING: Dependency installation failed, continuing..."
                    }
                }
            }
        }

        stage('Run Tests in Parallel') {
            parallel {
                stage('Default Tests') {
                    steps {
                        script {
                            try {
                                if (env.CHANGE_ID) {
                                    githubNotify context: 'Build', status: 'PENDING', description: 'Running default tests...'
                                }
                            } catch (err) {
                                echo "WARNING: githubNotify failed to send pending: ${err.getMessage()}"
                            }

                            def status = sh(script: "${PYTHON} run_tests.py --test_suite regression --env staging", returnStatus: true)

                            if (status == 0) {
                                try {
                                    if (env.CHANGE_ID) {
                                        githubNotify context: 'Build', status: 'SUCCESS', description: 'Default tests passed.'
                                    }
                                } catch (err) {
                                    echo "WARNING: githubNotify failed to send success: ${err.getMessage()}"
                                }
                            } else {
                                try {
                                    if (env.CHANGE_ID) {
                                        githubNotify context: 'Build', status: 'FAILURE', description: 'Default tests failed.'
                                    }
                                } catch (err) {
                                    echo "WARNING: githubNotify failed to send failure: ${err.getMessage()}"
                                }
                                error("Default tests failed")
                            }
                        }
                    }
                }

                stage('ATP Tests') {
                    steps {
                        script {
                            try {
                                if (env.CHANGE_ID) {
                                    githubNotify context: 'ATP Tests', status: 'PENDING', description: 'Running ATP tests...'
                                }
                            } catch (err) {
                                echo "WARNING: githubNotify failed to send pending: ${err.getMessage()}"
                            }

                            def atpStatus = sh(script: "${PYTHON} atp_test_runner.py --mode full", returnStatus: true)

                            if (atpStatus == 0) {
                                try {
                                    if (env.CHANGE_ID) {
                                        githubNotify context: 'ATP Tests', status: 'SUCCESS', description: 'ATP tests passed.'
                                    }
                                } catch (err) {
                                    echo "WARNING: githubNotify failed to send success: ${err.getMessage()}"
                                }
                            } else {
                                try {
                                    if (env.CHANGE_ID) {
                                        githubNotify context: 'ATP Tests', status: 'FAILURE', description: 'ATP tests failed.'
                                    }
                                } catch (err) {
                                    echo "WARNING: githubNotify failed to send failure: ${err.getMessage()}"
                                }
                                error("ATP tests failed")
                            }
                        }
                    }
                }

                post {
                        success {
                            script {
                                echo "✅ Final build status: SUCCESS"
                                currentBuild.result = 'SUCCESS'
                            }
                        }
                        failure {
                            script {
                                echo "❌ Final build status: FAILURE"
                                currentBuild.result = 'FAILURE'
                            }
                        }
                    }

            }
        }
    }
}
