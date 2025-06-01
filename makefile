rootdir = $(realpath .)
parentdir = $(realpath ..)
homedir = ${HOME}
env_file = ${parentdir}/env/.env.local

setup:
	@pip install -r requirements.txt

run:   ## run app locally, limit message size to 30MB, money is tight right now
	@USE_AGGRID=1 streamlit run about_daniel_belay.py --server.maxMessageSize=30000000

run_app:
	@streamlit run about_daniel_belay.py

docker_build:  ## build docker image for app
	@docker build -f Dockerfile . -t about_daniel_belay

docker_run:  ## run dashboard locally with docker (prereq: `make docker_build`)
	@docker run -p 8501:8501 \
		-v ${homedir}/gcp_service_account/keys:/gcloud \
		-v ${rootdir}/data:/app/data \
		-e GOOGLE_APPLICATION_CREDENTIALS=/gcloud/adc.json \
		about_daniel_belay

clean:
	rm -rf __pycache__
	rm -rf .streamlit
	rm -rf .DS_Store
	rm -rf .venv
	rm -rf .pytest_cache