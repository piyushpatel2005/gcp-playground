# Google Kubernetes Engine

GKE provides two types of clusters. Standard and Autopilot mode. In Standard, cluster we have to take care of autoscaling of nodes and we have choices on nodes and types whereas on Autopilot cluster, Google manages autoscaling and we pay per pod usage.

1. Standard cluster: In this we can specify Zonal or Regional (we can specify multiple zones). This will ensure that it is fault-tolerant at zonal level. We can choose fixed Control plane version using static channel or using Release channel it will provide latest stable Kubernetes versions. We can also configure initial node pool name and other settings like how many nodes to start with. We can enable Autoscaler even in standard cluster with certain limits on number of nodes to control costs. For upgrade, it has Surge Upgrade where single node is created additional and one node at a time is upgrade and it has Blue Green Upgrade which is production grade in which new nodepool is created and old nodepool is also kept running. This is also used when nodes need to be recreated. Once you're happy with configurations, click CREATE button.

## Deploy using Terraform


```shell
terraform init
export GOOGLE_PROJECT=<PROJECT_ID>
terraform plan -var project_id=$GOOGLE_PROJECT
terraform apply -var project_id=$GOOGLE_PROJECT -auto-approve
terraform destroy -var project_id=$GOOGLE_PROJECT -auto-approve
```

## Connecting to the cluster

Click three vertical dots and click Connect. It will give command used to connect to the cluster. Run this command and this will create a `.kube/config` file locally which will have the credentials for connecting to the Kubernetes.

```shell
gcloud config set project $PROJECT_ID
gcloud container clusters get-credentials [cluster-name] --region us-central1 --project $PROJECT_ID
kubectl version
kubectl get nodes
kubectl get pods -n kube-system
```

```shell
kubectl apply -f examples/01-demo-gcp-app
kubectl get deployment
kubectl get pod
kubectl get services
# Hit the external IP address.
kubectl delete -f examples/01-demo-gcp-app
```

In above app, the service will determine corresponding deployment using labels. This new deployment can be viewed under `Workloads` and `Service & Ingress` section in the GCP Console. The load balancer creates Load Balancer in the GCP services.

Install `google-cloud-sdk`, `kubectl` and `gke-gcloud-auth-plugin` tools in your terminal.

```shell
sudo snap install google-cloud-sdk --classic
sudo apt-get remove  google-cloud-sdk-gke-gcloud-auth-plugin
sudo snap install kubectl --classic
```

`kubectl` version must be one minor version different of your Kubernetes control plane version. Remvoe the existing KUBECONFIG using `rm $HOME/.kube/config`

```shell
kubectl config view
# once kubeconfig is configured, you can use below command to see client and cluster versions
kubectl version --output=yaml
```

## Creating resources imperatively (using CLI)
### Pod

```shell
# Deploy pod
kubectl run <pod_name> --image <container-image>
kubectl get pods # kubectl get po
kubectl get pods -o wide # get node information along with pod
kubectl describe pod <pod_name> # shows sequence of events that happend behind the scene
kubectl delete pod <pod_name>
```

### Services

This is to expose application running in pod.
- ClusterIP: expose internal to K8s cluster
- NodePort: expose internet or internal
- LoadBalancer: internet or internal. This create GCP load balancer. It will have port and targetport which represents K8s service port and target pod port.
- Ingress: internet or internal

```shell
kubectl run <pod-name> --image <container-image> # this pod has app running on port 80
kubectl expose pod <pod-name> --type=LoadBalancer --port=80 --name=<service-name>
kubectl get service # kubectl get svc
kubectl describe svc <service-name>
kubectl logs <pod-name>
kubectl logs --tail=20 <pod-name> # last 20 lines
kubectl logs --since=1h <pod-name> # last hour logs
kubectl logs -p -c <container-name> <pod-name> # return snapshot of previous terminated container logs from pod
kubectl logs -f <pod-name> # stream logs
kubectl exec -it <pod-name -- /bin/bash
kubectl exec -it <pod-name> /bin/bash
kubectl exec -it <pod-name -- cat /somefile/path # run command without opening active session
kubectl get pod <pod-name> -o yaml # yaml output of pod resource
kubectl get all
kubectl delete pod <pod-name>
kubectl delete svc <service-name>
```

### ReplicaSet

provides reliability, High availability, uses labels and selectors to connect everything together. There is no command to create Replicaset imperatively. This also creates load balancer by default.

```shell
cd examples/02-replicaset
kubectl create -f 01-replicaset.yaml
kubectl get replicaset # kubectl get rs
kubectl describe rs <replicaset-name>
kubectl get pods
kubectl get pod <pod-name> -o yaml # under ownerReferences it points to replicaset that created it.
kubectl expose rs <replica-set> --type=LoadBalancer --port=80 --target-port=8080 --name=<service-name> # expose replicaset using load balancer
kubectl get svc # http://<external-IP>/hello
kubectl delete pod <pod-name> # delete one of the pods, it will auto-create new one
# change replicas count from 3 to 5 in 01-replicaset.yaml to verify scalability
kubectl replace -f 01-replicaset.yaml
kubectl get po # it should show 5 replicas instead of 3, we can revert back to 3
kubectl delete rs <replicaset-name> # delete service and their pods
kubectl delete svc <service-name>
```

### Deployment
Deployment includes Replicaset. It is child of deployment.

```shell
kubectl create deployment <deployment-name> --image <container-image> # Create deployment
kubectl get deployments # kubectl get deploy
kubectl describe deploy <deployment-name>
kubectl get rs
kubectl get pods
kubectl get pod <pod-name> -o yaml # Owner reference should point to replica set above
# Update deployment
kubectl rollout history deployment/<deployment-name>
kubectl annotate deployment/<deployment-name> kubernetes.io/change-cause="Deployemtn Create - App version 1.0.0"
kubectl rollout history deployment/<deployment-name> # check history
# Scaling Deployment
kubectl scale --replicas=2 deployment/<deployment-name>
kubectl get pods
kubectl get deploy
kubectl get rs
kubectl scale --replicas=2 deployment/<deployment-name>
# Expose deployment
kubectl expose deployment <deployment-name> --type=LoadBalancer --port=80 --target-port=80 --name <service-name>
kubectl get svc # http://<external-ip>
# Update application version using new image (set image)
kubetl get deployment <deployment-name> -o yaml
kubectl set image deployment/<deployment-name> <container-name>=<new-container-image> --record=true
kubectl rollout status deployment/<deployment-name>
kubectl rollout history deployment/<deployment-name>
kubectl describe deployment <deployment-name> 
kubectl get rs # 2 replica set, one with 0/0 for older container-image
# Access new application with version 2.
kubectl annotate deployment/<deployment-name> kubenetes.io/change-cause="Deployment Update - App version 2.0.0"
# Update application version using edit deployment
kubectl edit deployment/<deployment-name>
# Modify spec.containers.image to newer version
kubectl rollout status deployment/<deployment-name>
kubectl annotate deployment/<deployment-name> kubernetes.io/change-cause="Deployment Update - App version 3.0.0"
# Rollback to previous version of application
kubectl rollout history deployment/<deployment-name>
kubectl rollout history deployment/<deployment-name> --revision=1 # check what image was used for a version
kubectl rollout undo deployment/<deployment-name> # rollback to previous version
# Rollback to specific version of the application
kubectl rollout undo deployment/<deployment-name> --to-revision=<revision-number>
# Perform rolling restart of application
kubectl rollout restart deployment/<deployment-name>
# Pause and Resume deployment. This may be for maintenance or making bigger changes.
kubectl rollout pause deployment/<deployment-name>
kubectl set image deployment/<deployment-name> kubenginex=<container-image> # This doesn't deploy new version of pods
kubectl set resources deployment/<deployment-name> -c=kubenginx --limits=cpu=20m,memory=30Mi
kubectl rollout resume deployment/<deployment-name> # This is when deployment actually happens and new revision is created in rollout history
kubectl rollout history deployment/<deployment-name>
kubectl delete deploy <deployment-name>
kubectl delete svc <service-name>
```

## Creating resources in Declarative manner