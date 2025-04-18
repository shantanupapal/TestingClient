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

                stage('Run ATP Tests') {
                    steps {
                        script {
                            def testPassed = true
                            try {
                                sh """
                                    echo "Running ATP sample tests"
                                    docker run --rm \
                                        --mount type=bind,source=\$WORKSPACE/main/tests/atp,target=/tests \
                                        ${env.IMAGE_NAME}:latest \
                                        sh -c 'cd /tests && pytest --junitxml=atp_results.xml'
                                """
                            } catch (err) {
                                testPassed = false
                                throw err  // to fail the stage
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
