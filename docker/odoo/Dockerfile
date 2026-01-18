# Sử dụng base image chính chủ từ Odoo
FROM odoo:19.0

USER root

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

RUN mkdir -p /mnt/extra-addons \
    && chown -R odoo:odoo /mnt/extra-addons
RUN mkdir -p /mnt/odoo-addons \
    && chown -R odoo:odoo /mnt/odoo-addons

USER odoo