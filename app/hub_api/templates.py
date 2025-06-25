from jinja2 import Template

s3 = '''
---
apiVersion: s3.aws.upbound.io/v1beta1
kind: Bucket
metadata:
  name: {{ meta.name }}
spec:

  forProvider:
    region: {{ region_name }} # only us-east-2 works
  providerConfigRef:
    name: aws-default
  deletionPolicy: Delete

'''