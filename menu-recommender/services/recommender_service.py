import torch
from torch.functional import F


class RecommenderService:
    def __init__(self, model, recipe_embeddings, ingredient_vocab, recipe_dataset):
        self.model = model
        self.recipe_embeddings = recipe_embeddings
        self.ingredient_vocab = ingredient_vocab
        self.recipe_dataset = recipe_dataset

    def get_recommendations(self, ingredients: list[str], top_k=3) -> list:
        # Create query embedding
        query_recipe_ingredients = [self.ingredient_vocab[i] for i in ingredients]
        query_embedding = self.model([query_recipe_ingredients])

        # Calculate the topk
        similarity = F.cosine_similarity(query_embedding, self.recipe_embeddings)
        top_k = torch.topk(similarity, k=top_k)
        results = [(idx.item(), similarity[idx].item()) for idx in top_k.indices]

        recipe_recommendations = list()
        for idx, score in results:
            recipe = self.recipe_dataset.iloc[idx]
            recipe_recommendations.append(
                {
                    "title": recipe["title"],
                    "ingredients": recipe["NER"],
                }
            )

        return recipe_recommendations
