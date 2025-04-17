pipeline {
    agent any

    stages {
        stage('Test GitHub Notify') {
            steps {
                script {
                    githubNotify context: 'Check Notify', status: 'PENDING', description: 'Sending notify test...'
                    echo "✔ githubNotify works! yeah"
                    githubNotify context: 'Check Notify', status: 'SUCCESS', description: 'Notify succeeded!'
                }
            }
        }
    }
}
