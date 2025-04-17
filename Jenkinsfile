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

                    def depStatus = sh(script: '''
                        which python3 || true
                        python3 -m pip install --upgrade pip || true
                        if [ -f requirements.txt ]; then python3 -m pip install -r requirements.txt || true; fi
                    ''', returnStatus: true)

                    if (depStatus == 0) {
                        githubNotify context: 'Build', status: 'SUCCESS', description: 'Dependencies installed.'
                    } else {
                        githubNotify context: 'Build', status: 'FAILURE', description: 'Dependency install failed.'
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

                stage('ATP Tests') {
                    steps {
                        script {
                            githubNotify context: 'ATP Tests', status: 'PENDING', description: 'Running ATP tests...'

                            def atpStatus = sh(script: "${PYTHON} atp_test_runner.py --mode full", returnStatus: true)

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
    }
}