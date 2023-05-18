import json
import csv
from googleapiclient.discovery import build

# Read the candidate list from the CSV file
with open('senate_candidate_2022.csv', 'r') as f:
    candidates = [line.strip().split(',') for line in f.readlines()]
with open('senators_list.csv', 'r') as f:
    senators = [line.strip().split(',') for line in f.readlines()]

politicians = []

points = {
    "Pants on Fire": 5,
    "Four Pinocchios": 5,
    "False": 4,
    "Three Pinocchios": 4,
    "Mostly False": 3,
    "Two Pinocchios": 3,
    "Half True": 2,
    "One Pinocchio": 2,
    "Mostly True": 1,
    "Outdated": 2,
    "Distorts the Facts": 4,
    "Lacks Context": 3,
    "Spins the Facts": 3,
    "Not the Whole Story": 2,
    "Flip- Flop": 1
}

for candidate in candidates:
    name, party, state, win = candidate
    politicians.append(name)

for senator in senators:
    name, party, state = senator
    if name not in politicians:
        politicians.append(name)
politicians.sort()
#for politician in politicians:
#    print(politician)
#print(len(politicians))


# Set up the service
service = build('factchecktools', 'v1alpha1', developerKey='AIzaSyC9Arp-_WNFdp6zPSKxNAflDSxhWOouRkY')
topics = ['abortion', 'guns','health care', 'taxes', 'immigration', 'climate']
results = []
# Iterate over each candidate
for topic in topics:
    print(topic)
    for politician in politicians:
        #print(candidate)
        #name, party, state, win = candidate
        query = politician + " " + topic
        #print(politician + " done.")
        # Iterate over each tweet
        # Call the API to fact-check the claim
        response = service.claims().search(query=query).execute()
        #print(response)
        result={}
        # Check if there are any claims for the tweet
        if 'claims' in response:
            # Iterate over each claim
            for claim in response['claims']:
                # Check if the candidate is the claimant
                #print(politician + " " + )
                if claim.get('claimant', '') == politician and claim['claimReview'][0]['textualRating'] not in ['True', 'McCain Was Anomaly']:
                    result = {
                        'Name': politician,
                        'Claim': claim['text'],
                        'Source': claim['claimReview'][0]['publisher']['name'],
                        'Rating': claim['claimReview'][0]['textualRating'],
                        'Score': points[claim['claimReview'][0]['textualRating']],
                        'URL': claim['claimReview'][0]['url'],
                        'Date': claim['claimDate']
                        }
                    results.append(result)
                    #print(result)
                
    # Write the results to separate JSON files
    #print(result)
    fieldnames=['Name','Claim','Source','Rating','Score', 'URL','Date']
    if results:
        with open(f'{topic}.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
            #json.dump(results, f)
        print("All Results for "+ topic +" written to file.")
    else:
        print("No results found for this set.")