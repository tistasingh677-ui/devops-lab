pipeline {
    agent any
    environment {
        DOCKERHUB_USER = 'komals677'
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Build Imags') {
            steps {
                sh 'docker biuld -t $DOCKERHUB_USER/producer:$BUILD_NUMBER ./producer'
                sh 'docker build -t $DOCKERHUB_USER/consumer:$BUILD_NUMBER ./consumer'
            }
        }
        stage('Push Images') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh 'echo $PASS | docker login -u $USER --password-stdin'
                    sh 'docker push $DOCKERHUB_USER/producer:$BUILD_NUMBER'
                    sh 'docker push $DOCKERHUB_USER/consumer:$BUILD_NUMBER'
                }
            }
        }
        stage('Deploy') {
            steps {
                sh 'kubectl set image deployment/producer producer=$DOCKERHUB_USER/producer:$BUILD_NUMBER'
                sh 'kubectl set image deployment/consumer consumer=$DOCKERHUB_USER/consumer:$BUILD_NUMBER'
                sh 'kubectl rollout status deployment/producer'
                sh 'kubectl rollout status deployment/consumer'
            }
        }
    }
}
