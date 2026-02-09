def skill_action(skill: str) -> str:
    s = skill.lower()

    # ----- Tier 1: Explicit high-value skills -----
    if s in ["docker", "kubernetes"]:
        return (
            "Add containerization experience. Mention Dockerizing an existing project "
            "or deploying a service using containers."
        )

    if s in ["pytorch", "tensorflow"]:
        return (
            "Highlight hands-on model training and inference. "
            "Mention architectures, training loops, or evaluation steps."
        )

    if s in ["sql"]:
        return (
            "Explicitly mention SQL queries, joins, aggregations, and real datasets used."
        )

    if s in ["spark", "pyspark"]:
        return (
            "Emphasize distributed data processing, Spark SQL usage, "
            "and performance optimization."
        )

    # ----- Tier 2: Category-based patterns -----
    if s in ["aws", "azure", "gcp"]:
        return (
            "Highlight cloud-based architecture. Mention services used, "
            "data storage, deployment, or scalability aspects."
        )

    if "cloud" in s:
        return (
            "Describe how you used cloud infrastructure for scalability, storage, "
            "or deployment."
        )

    if s in ["airflow", "prefect", "dagster"]:
        return (
            "Mention workflow orchestration, scheduling, and pipeline reliability."
        )

    if s in ["kafka", "rabbitmq"]:
        return (
            "Highlight real-time or streaming data processing and system integration."
        )

    # ----- Tier 3: Safe fallback -----
    return (
        f"Consider explicitly describing how you used **{skill}**, "
        "what problem it solved, and the impact it had."
    )
