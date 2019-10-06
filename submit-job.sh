REGION=us-central1
CLUSTER=cluster-a422
BUCKET=dataproc-76399b63-8b38-4f0a-b831-6e680daa45e8-us-central1

helpFunction()
{
   echo ""
   echo "Usage: $0 -f fileName.py"
   echo -e "\t-f Name of the python file to be submitted to the cluster"
   exit 1 # Exit script after printing help
}

while getopts "f:" opt
do
   case "$opt" in
      f ) parameterF="$OPTARG" ;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done

# Print helpFunction in case parameters are empty
if [ -z "$parameterF" ]
then
   echo "Some or all of the parameters are empty";
   helpFunction
fi

echo ""
echo "> Removing output directory from REMOTE storage..."
echo ""
gsutil -m rm -r gs://$BUCKET/output
echo ""
echo "> Submiting $parameterF as a job to the cluster..."
echo ""
gcloud dataproc jobs submit pyspark $parameterF --region=$REGION --cluster=$CLUSTER
echo ""
echo "> Downloading output directory from REMOTE storage to LOCAL storage..."
echo ""
gsutil -m cp -r gs://$BUCKET/output ./storage/$BUCKET/