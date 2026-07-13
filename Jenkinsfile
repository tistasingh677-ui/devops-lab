pipeline {
    agent any
    environment {
        DOCKERHUB_USER = 'komals677'
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Build Images') {
            steps {
                sh 'docker build -t $DOCKERHUB_USER/producer:$BUILD_NUMBER ./producer'
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
    }
}
