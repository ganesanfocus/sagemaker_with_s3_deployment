import sagemaker
import traceback

def delete_endpoints():
    try:
        # Initialize SageMaker session
        session = sagemaker.Session()
        
        # Delete the endpoint
        endpoint_name = "insurance-charge-endpoint031"
        session.delete_endpoint(endpoint_name)
        
        # Also delete the endpoint configuration (optional but recommended to avoid charges)
        session.delete_endpoint_config(endpoint_name)
        return "successfully deleted"
    except Exception as e:
        print(traceback.format_exc())
        return str(e)

if __name__ == "__main__":
    result = delete_endpoints()
    print(result)