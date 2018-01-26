# cudamon
NVIDIA Cuda Monitor

# Summary
CUDAMon is an NVIDIA GPU monitor with the ability to notify on problematic events. CUDAMon is configured to monitor a metric against a threshold, then notify you incase that threshold is surpassed. Supported metrics:
- Temperature
- Utilization

## Dependencies:
- Docker-CE (17.02+ recommeded)
- [NVIDIA-Docker](https://github.com/NVIDIA/nvidia-docker)
- AWS Account (for access to SNS)

## Environment Variables:
- `TIMEOUT_MINS`: The length of time in minutes between notification alerts. Default 10.
- `POLL_SECS`: The length of time in seconds between each nvidia-smi poll. Default 60.
- `GPU_UTIL_<ARCH>`: The utilization threshold that the specific GPU model must stay above. Default 80.
- `GPU_TEMP_<MODEL>`: The temperature threshold that the specific GPU model must stay below. Default 75.
- `SNS_TOPIC_ARN`: The AWS SNS topic ARN to publish to. Note: SNS messages are published in `raw` message structure.
- `AWS_ACCESS_KEY_ID`: The AWS Access Key ID /w publish access to the SNS topic `${SNS_TOPIC_ARN}`.
- `AWS_SECRET_ACCESS_KEY`: The AWS Secret Access Key associated with `${AWS_ACCESS_KEY_ID}`.

# Run
```
docker run -d --name cudamon \
--runtime=nvidia \
-e TIMEOUT_MINS=10 \
-e POLL_SEC=15 \
-e GPU_UTIL_1070=90 \
-e GPU_UTIL_1080=90 \
-e GPU_TEMP_1080_TI=85 \
-e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
-e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
-e SNS_TOPIC_ARN=${SNS_TOPIC_ARN} \
djenriquez/cudamon
```

## Donations
- BTC - 33DyXVuy3R5jfLZRRpEQcXXAJ1Xz5rkGxE
- LTC - MUaov1JidbnpfeuQiSR3mtJhN3CN8Wj5g9
- ETH - 0xCBBC579Ac1Bc4868823fbBb2D8dDaFF93D619ceD
- DASH - Xy4cgJVAiHsrbeBB53NeQWk2iXKoWjBvJp
- ZEC - t1gYs8Zn2ZCFZWKZsTmZWd5bgXa9eD8M87K
- BCH - LOL
