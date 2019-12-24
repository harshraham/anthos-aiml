#!/bin/bash

gcloud auth configure-docker
docker build -t loandefault:1.0.0 .
docker tag loandefault:1.0.0 us.gcr.io/anthos-setup-8be124/loandefault:1.0.0
docker push us.gcr.io/anthos-setup-8be124/loandefault:1.0.0

gcloud container clusters get-credentials kf-aiml --zone us-central1-a --project anthos-setup-8be124

kubectl delete -f deployment.yml -n anthos-aiml
kubectl delete -f ingress.yml -n anthos-aiml

kubectl apply -f deployment.yml -n anthos-aiml
kubectl apply -f ingress.yml -n anthos-aiml --validate=false