#from sentence_transformers import SentenceTransformer
import sentence_transformers
import scipy
#from sklearn.metrics.pairwise import cosine_similarity

model = sentence_transformers.SentenceTransformer('bert-base-nli-mean-tokens')

def sent_similarity(col_nouns, bok_noun):
    bok_nouns = bok_noun[0]
    sentence_embeddings_L1 = model.encode(bok_nouns[0])
    sentence_embeddings_L2 = model.encode(bok_nouns[1])
    sentence_embeddings_L3 = model.encode(bok_nouns[2])
    #sentence_embeddings_L4a = model.encode(bok_nouns[3])
    #sentence_embeddings_L4b = model.encode(bok_nouns[4])

    #sent_embed_bok_levels = [sentence_embeddings_L1, sentence_embeddings_L2, sentence_embeddings_L3, sentence_embeddings_L4a, sentence_embeddings_L4b]
    sent_embed_bok_levels = [sentence_embeddings_L1, sentence_embeddings_L2, sentence_embeddings_L3]
    noun_levels = []
    unClassified = []
    for i in range(len(col_nouns)):
        tier_nouns = [[], [], [], [], []]
        for query in col_nouns[i]:
            queries = [query]
            query_embeddings = model.encode(queries)
            for query, query_embedding in zip(queries, query_embeddings):
                prev_dist = 0;
                isClassified = False;
                for indx, sentence_embeddings in enumerate(sent_embed_bok_levels):
                    distances = scipy.spatial.distance.cdist([query_embedding], sentence_embeddings, "cosine")[0]
                    #distances = cosine_similarity([query_embedding], sentence_embeddings)[0]
                    results = zip(range(len(distances)), distances)
                    results = sorted(results, key=lambda x: x[1])
                    distance = 1 - results[0][1]
                    print(query, "tier: ",indx ,"(Cosine Score: %.4f)" % (distance))
                    if (distance > prev_dist and distance > 0.40):
                        prev_dist = distance
                        tier_nouns[indx].append(query)
                        isClassified = True;
                if isClassified == False:
                    unClassified.append(query)
        noun_levels.append(tier_nouns)

    print("Categorized nouns", noun_levels, " Uncategorized Nouns: ", unClassified)
    return noun_levels
