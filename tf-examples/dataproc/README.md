# Dataproc

Dataproc is GCP's managed Hadoop cluster service with optional components like zeppelin, presto etc.

## Create single node cluster without metastore.

Below is for experimental or evaluation purpose only because it does not have high availability.

```shell
gcloud dataproc clusters create demo-cluster --region us-central1 --subnet default --zone us-central1-a --single-node --master-machine-type n2-standard-4 --master-boot-disk-size 300 --image-version 2.0-debian10 --optional-components ZOOKEEPER --project $PROJECT_ID
```

In order to get access to some of the open source tools' web interface, we may have to enable component gateway. Following are the things which provide access to web interfaces.
1. Component web interfaces can be accessed by users who have `dataproc.clusters.use` IAM permission.
2. Component Gateway can be used to access REST APIs, such as Apache Hadoop YARN and Apache Livy, and history servers.
3. When Component Gateway is enabled, the first master node in the cluster will have the following additional services: Apache Knox and Inverting Proxy
4. Component gateway does not enable direct access to `node:port` interfaces, but proxies a specific subset of services automatically. If you want to access services on nodes (`node:port`), use an `SSH SOCKS` proxy.

for using components gateway, we have to add flag `--enable-component-gateway` to cluster creation command.

```shell
# Create cluster with component gateway enabled
gcloud dataproc clusters create demo-cluster --enable-component-gateway --region us-central1 --subnet default --zone us-central1-b --single-node --master-machine-type n2-standard-2 --master-boot-disk-size 300 --image-version 2.0-debian10 --optional-components ZEPPELIN --project $PROJECT_ID
# Delete the cluster
gcloud dataproc clusters delete demo-cluster --project $PROJECT_ID --region us-central1
```

In order to connect to web interfaces like Zeppelin, we have to connect an SSH tunnel to use from localhost.

```shell
gcloud compute ssh cluster-705f-m \
  --project=playground-s-11-b7abc5f9 \
  --zone=us-central1-a -- -D 1080 -N
```

## High availability cluster creation

