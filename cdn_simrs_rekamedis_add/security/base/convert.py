import csv

addons      =   'cdn_simrs_rekamedis_add'
input_csv   =   f"/home/diavolo/Documents/odoo/v18_odoo/addons/v18_simrs_add/{addons}/security/ir.model.access.csv"
output_csv  =   f"/home/diavolo/Documents/odoo/v18_odoo/addons/v18_simrs_add/{addons}/security/base/ir.model.access.csv"

template = {
    "create": (0, 0, 1, 0, "cdn_base.group_create_cdn_database"),
    "read":   (1, 0, 0, 0, "cdn_base.group_read_cdn_database"),
    "write":  (0, 1, 0, 0, "cdn_base.group_write_cdn_database"),
    "unlink": (0, 0, 0, 1, "cdn_base.group_unlink_cdn_database"),
}

result = []
exist_check = set()   # untuk mencegah duplikat ID

with open(input_csv, newline="") as f:
    reader = csv.reader(f)

    for row in reader:
        if not row or len(row) == 0:
            continue

        if row[0] == "id":
            continue  # skip header

        model = row[2]  # kolom model_id:id
        base = "access_model_" + model.replace(".", "_")

        for action, (r, w, c, u, group) in template.items():
            new_id = f"{base}_{action}"
            new_name = new_id

            # Cegah duplikat
            if new_id in exist_check:
                continue

            exist_check.add(new_id)

            result.append([
                new_id,
                new_name,
                model,
                group,
                r, w, c, u
            ])

# Tulis hasil CSV
with open(output_csv, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "id", "name", "model_id:id", "group_id:id",
        "perm_read", "perm_write", "perm_create", "perm_unlink"
    ])
    writer.writerows(result)

print("DONE! File saved:", output_csv)
