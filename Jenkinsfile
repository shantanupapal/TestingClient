pipeline {
    agent any

    environment {
        PYTHON = 'python3'
    }

    stages {
        stage('Install Dependencies') {
            steps {
                script {
                    echo "Installing Python dependencies"

                    def depStatus = sh(script: '''
                        which python3 || true
                        python3 -m pip install --upgrade pip || true
                        if [ -f requirements.txt ]; then python3 -m pip install -r requirements.txt || true; fi
                    ''', returnStatus: true)

                    if (depStatus == 0) {
                        echo "Dependencies installed successfully."
                    } else {
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
                            def testPassed = true
                            try {
                                sh "${PYTHON} run_tests.py --test_suite regression --env staging"
                            } catch (err) {
                                testPassed = false
                                throw err
                            } finally {
                                publishChecks name: 'Default Tests',
                                              conclusion: testPassed ? 'SUCCESS' : 'FAILURE'
                            }
                        }
                    }
                }

                stage('Run ATP Tests') {
                    steps {
                        script {
                            def testPassed = true
                            try {
                                sh """
                                    echo "Running ATP tests from atp_test_runner.py"
                                    docker run --rm \
                                        --mount type=bind,source=\$WORKSPACE,target=/app \
                                        ${env.IMAGE_NAME}:latest \
                                        sh -c 'cd /app && python3 atp_test_runner.py'
                                """
                            } catch (err) {
                                testPassed = false
                                throw err
                            } finally {
                                publishChecks name: 'ATP Tests',
                                            conclusion: testPassed ? 'SUCCESS' : 'FAILURE'
                            }
                        }
                    }
                }

            }
        }
    }
}
