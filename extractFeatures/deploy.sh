aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 621130241729.dkr.ecr.us-east-1.amazonaws.com
docker build -t extractfeatures .
docker tag extractfeatures:latest 621130241729.dkr.ecr.us-east-1.amazonaws.com/extractfeatures:latest
docker push 621130241729.dkr.ecr.us-east-1.amazonaws.com/extractfeatures:latest
aws lambda update-function-code \
           --function-name extractfeatures \
           --image-uri 621130241729.dkr.ecr.us-east-1.amazonaws.com/extractfeatures:latest
docker image prune -a --force
docker system prune -a -y