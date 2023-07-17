aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 621130241729.dkr.ecr.us-east-1.amazonaws.com
docker build -t accessdb .
docker tag accessdb:latest 621130241729.dkr.ecr.us-east-1.amazonaws.com/accessdb:latest
docker push 621130241729.dkr.ecr.us-east-1.amazonaws.com/accessdb:latest
aws lambda update-function-code \
           --function-name accessDB \
           --image-uri 621130241729.dkr.ecr.us-east-1.amazonaws.com/accessdb:latest
docker image prune -a --force
docker system prune -a -y