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
                                echo "Running ATP tests from atp_test_runner.py"
                                sh """
                                    ${env.PYTHON} atp_test_runner.py
                                """
                            } catch (err) {
                                testPassed = false
                                // still fail the stage
                                throw err
                            } finally {
                                withCredentials([string(credentialsId: 'github-token', variable: 'GITHUB_TOKEN')]) {
                                    def state = testPassed ? "success" : "failure"
                                    def desc = testPassed ? "ATP tests passed" : "ATP tests failed"
                                    def commitSha = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()

                                    sh """
                                        curl -s -X POST \
                                            -H "Authorization: token \$GITHUB_TOKEN" \
                                            -H "Content-Type: application/json" \
                                            -d '{
                                                "state": "$state",
                                                "context": "ATP Tests",
                                                "description": "$desc",
                                                "target_url": "${env.BUILD_URL}"
                                            }' \
                                            https://api.github.com/repos/shantanupapal/TestingClient/statuses/$commitSha
                                    """
                                }
                            }
                        }
                    }
                }



            }
        }
    }
}
