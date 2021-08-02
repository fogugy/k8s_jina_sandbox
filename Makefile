build-image:
	docker build -t jina-base:latest -f ./jina.dockerfile . &&\
	docker tag jina-base:latest us-central1-docker.pkg.dev/jina-sandbox/images/jina-base:latest &&\
	docker push us-central1-docker.pkg.dev/jina-sandbox/images/jina-base

deploy:
	kubectl apply -f ./k8s/storage-class.yaml &&\
	kubectl apply -f ./k8s/index-pvc.yaml &&\
	kubectl apply -f ./k8s/configmap.yaml &&\
	kubectl apply -f ./k8s/service_gateway.yaml &&\
	kubectl apply -f ./k8s/service_expose.yaml &&\
	kubectl apply -f ./k8s/service_pod0.yaml &&\
	kubectl apply -f ./k8s/service_pod1.yaml &&\
	kubectl apply -f ./k8s/deployment_gateway.yaml &&\
	kubectl apply -f ./k8s/deployment_pod0.yaml &&\
	kubectl apply -f ./k8s/deployment_pod1.yaml

