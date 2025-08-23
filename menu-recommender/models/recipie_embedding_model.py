import torch
import torch.nn as nn
import torch.nn.functional as F

class RecipeEmbeddingModel(nn.Module):
    def __init__(self, vocab_size, embedding_dim):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)

    def forward(self, ingredient_indices):
        # Pad variable-length ingredient lists
        padded = nn.utils.rnn.pad_sequence(
            [torch.tensor(x) for x in ingredient_indices],
            batch_first=True
        )
        mask = (padded != 0)  # padding mask
        embeds = self.embedding(padded)

        # Mean pooling over ingredients
        masked_embeds = embeds * mask.unsqueeze(-1)
        recipe_embeds = masked_embeds.sum(1) / mask.sum(1, keepdim=True)

        # normalize for cosine similarity
        recipe_embeds = F.normalize(recipe_embeds, dim=-1)
        return recipe_embeds