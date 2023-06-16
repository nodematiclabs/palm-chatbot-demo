# Custom Chatbot App on GCP

1. Setup a Kubernetes cluster (e.g., GKE Autopilot) for your app and configure `kubectl` to use it
1. Setup a `chatbot` Cloud Armor policy, and think about your broader security strategy
1. Set an environment variable for your google project (used in subsequent steps)
    ```bash
    export GOOGLE_PROJECT=your-project-here
    ```
1. Create a static IP for your networking frontend
    ```bash
    gcloud compute addresses create chatbot --project=$GOOGLE_PROJECT --global
    ```
1. Setup IAM RBAC resources
    ```bash
    gcloud iam service-accounts create chatbot \
        --project=$GOOGLE_PROJECT
    gcloud projects add-iam-policy-binding $GOOGLE_PROJECT \
        --member "serviceAccount:chatbot@$GOOGLE_PROJECT.iam.gserviceaccount.com" \
        --role "roles/aiplatform.user"
    gcloud iam service-accounts add-iam-policy-binding chatbot@$GOOGLE_PROJECT.iam.gserviceaccount.com \
        --role roles/iam.workloadIdentityUser \
        --member "serviceAccount:$GOOGLE_PROJECT.svc.id.goog[default/chatbot]"
    ```
1. Setup Kubernetes RBAC resources
    ```bash
    kubectl create serviceaccount chatbot
    kubectl annotate serviceaccount chatbot \
        iam.gke.io/gcp-service-account=chatbot@$GOOGLE_PROJECT.iam.gserviceaccount.com
    ```
1. Build and push your docker image (see the `Dockerfile` example)
1. Deploy your containerized app (see the `resources.yaml` example)