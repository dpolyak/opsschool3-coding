import json, yaml
import sys

DEBUG_MODE = False

#-----------------------------------------
def load_json_input_data(input_file):
    with open(input_file) as f:
       read_data = f.read()

    json_data = json.loads(read_data)

    return json_data

#-----------------------------------------
def create_buckets_groups_list(buckets):
	all_age_groups = []

	buckets.sort()
	buckets_length = len(buckets)

	if buckets_length >= 2:
		for i in range(0, buckets_length - 1):
			age_group = (buckets[i], buckets[i + 1])
			all_age_groups.append(age_group)

	return all_age_groups

#-----------------------------------------
def devide_people_by_buckets(people, buckets):
	youngest_bucket = []
	oldest_bucket = []

	buckets_list = create_buckets_groups_list(buckets)

	min_bucket_age = buckets_list[0][0]
	max_bucket_age = buckets_list[-1][-1]
	people_min_age = min_bucket_age
	people_max_age = max_bucket_age
	people_by_group_list = list()

	#init list of people devided by age buckets
	for i in buckets_list:
		people_by_group_list.append( list() )

	# devide people by buckets
	for name, age in people.items():
		group_id = 0
		found_bucket = False

		for age_group in buckets_list:
			if age in range(age_group[0], age_group[1]):
				if not DEBUG_MODE:
					people_by_group_list[group_id].append(name)
				else:
					people_by_group_list[group_id].append(age)
				found_bucket = True
			group_id += 1

		# update oldest and youngest extra buckets
		if not found_bucket:
			if age > max_bucket_age:
				update_bucket(oldest_bucket, name, age)
				if age > people_max_age:
					people_max_age = age
			elif age < min_bucket_age:
				update_bucket(youngest_bucket, name, age)
				if age < people_min_age:
					people_min_age = age

	# add oldest and youngest extra buckets
	if people_min_age < min_bucket_age:
		buckets_list.insert( 0, (people_min_age, min_bucket_age) )
		people_by_group_list.insert(0, youngest_bucket)
	if people_max_age > max_bucket_age:
		buckets_list.append((max_bucket_age, people_max_age))
		people_by_group_list.append(oldest_bucket)
	
	
	return (buckets_list, people_by_group_list)

#-----------------------------------------	
def update_bucket(bucket, name, age):
	if not DEBUG_MODE:
		bucket.append(name)
	else:
		bucket.append(age)

#-----------------------------------------	
def write_to_yaml_file(buckets_list, people_by_buckets_list, file_name):

	buckent_dict = dict()
	buckets_names_list = []

	for gr in buckets_list:
		buckets_names_list.append( "%s-%s" % (gr[0], gr[1]) )

	for id in range(len(buckets_list)):
		buckent_dict.update( { buckets_names_list[id] : people_by_buckets_list[id] } )

	with open(file_name, 'w') as outfile:
		yaml.dump(buckent_dict, outfile, allow_unicode=True, default_flow_style=False)

#-----------------------------------------
if __name__ == "__main__":
    if len(sys.argv) >= 2:
    	if len(sys.argv) == 3:
    		DEBUG_MODE = sys.argv[2]

    	input_file_name = sys.argv[1]
    	output_file_name = input_file_name[:input_file_name.rfind('.')] + '.yaml'

    	input_data = load_json_input_data(input_file_name)
    	buckets = input_data['buckets']
    	people = input_data['ppl_ages']
    	
    	(buckets_list, people_by_group_list) = devide_people_by_buckets(people, buckets)
    	write_to_yaml_file(buckets_list, people_by_group_list, output_file_name)
    else:
        print(f"Input file name is missing:\n%s <data_file_name>" % sys.argv[0])
        