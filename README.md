# cudamon
NVIDIA Cuda Monitor

# Run
```
docker run -d --name cudamon \
--runtime=nvidia
-e POLL_SEC=15 \
-e GPU_UTIL_1070=90 \
-e GPU_UTIL_1080=90 \
-e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
-e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
-e SNS_TOPIC_ARN=${SNS_TOPIC_ARN} \
djenriquez/cudamon
```