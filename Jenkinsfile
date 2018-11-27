node{
    stage ("copy credentials"){
        withCredentials([sshUserPrivateKey(credentialsId: "aws_quantum", keyFileVariable: "FILE_AWS")]) {
	      sh "touch ~/.ssh/id_rsa"
        sh "mv $FILE_AWS ~/.ssh/id_rsa"
        sh 'echo "Host * \n' + 'StrictHostKeyChecking no" >> ~/.ssh/config'
       }
    }
    stage ("install pkg"){
      withCredentials([sshUserPrivateKey(credentialsId: "aws_quantum", keyFileVariable: "FILE_AWS")]) {
        sh "ssh ec2-user@10.10.5.48 sudo yum install git -y"
        sh "ssh ec2-user@10.10.5.48 sudo yum install docker -y"
        sh "ssh ec2-user@10.10.5.48 sudo pip install docker-compose"
        sh "ssh ec2-user@10.10.5.48 sudo service docker start"
        sh "ssh ec2-user@10.10.5.48 sudo chkconfig docker on"

        sh "ssh ec2-user@10.10.4.148 sudo yum install git -y"
        sh "ssh ec2-user@10.10.4.148 sudo yum install docker -y"
        sh "ssh ec2-user@10.10.4.148 sudo pip install docker-compose"
        sh "ssh ec2-user@10.10.4.148 sudo service docker start"
        sh "ssh ec2-user@10.10.4.148 sudo chkconfig docker on"
      }
    }

    stage ("get app files"){
      withCredentials([sshUserPrivateKey(credentialsId: "aws_quantum", keyFileVariable: "FILE_AWS")]) {
        checkout scm
        sh "scp -r * ec2-user@10.10.5.48:~/quantum-back/"
        sh "scp -r * ec2-user@10.10.4.148:~/quantum-back/"
        deleteDir()
      }
    }

    stage ("stop and start docker"){
      withCredentials([sshUserPrivateKey(credentialsId: "aws_quantum", keyFileVariable: "FILE_AWS")]) {
        //sh "ssh ec2-user@10.10.5.48 sudo docker stop \$(ssh ec2-user@10.10.5.48 sudo docker ps -a -q)"
        //sh "ssh ec2-user@10.10.5.48 sudo docker rm \$(ssh ec2-user@10.10.5.48 sudo docker ps -a -q)"
        //sh "ssh ec2-user@10.10.5.48 sudo docker rmi \$(ssh ec2-user@10.10.5.48 sudo docker images -q)"
        sh "ssh ec2-user@10.10.5.48 sudo /usr/local/bin/docker-compose -f ./quantum-back/docker-compose.yml down"
        sh "ssh ec2-user@10.10.5.48 sudo /usr/local/bin/docker-compose -f ./quantum-back/docker-compose.yml up --build -d"
        sh "ssh ec2-user@10.10.4.148 sudo /usr/local/bin/docker-compose -f ./quantum-back/docker-compose.yml down"
        sh "ssh ec2-user@10.10.4.148 sudo /usr/local/bin/docker-compose -f ./quantum-back/docker-compose.yml up --build -d"
      }
    }

}
