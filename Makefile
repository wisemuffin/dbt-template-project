# Regenerate the dbt manifest.json
dbt_manifest:
	dbt ls \
		--project-dir data-transformation/hacker_news_dbt \
		--profiles-dir data-transformation/hacker_news_dbt/config

dbt_manifest2:
	dbt ls \
		--project-dir data-transformation/fake_data_dbt \
		--profiles-dir data-transformation/fake_data_dbt/config
