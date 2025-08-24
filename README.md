# Menu Mingles

Menu Mingles is an experimental platform to help households plan weekly menus and generate shopping lists while accounting for guests, dietary restrictions, and balanced nutrition.  It combines multiple services so users can schedule meals, discuss plans with others, and receive recommendations that avoid repeating meat-heavy dishes or unsuitable ingredients.

## Pitch

Menu planning is time‑consuming, complicated and often leads to food waste. Creating a weekly plan means juggling preferences, intolerances, dietary goals and existing supplies—a process that quickly becomes a burden.

MenuMingles flips the script: instead of painstakingly writing lists, digital twins handle the planning. Each household member gets a profile that becomes a persona with goals, likes and intolerances. Virtual advisors such as an environmentalist and a Chef orchestrator join the discussion, debating menus on behalf of the household.

The smart fridge kicks things off when supplies run low, triggering MenuMingles to start planning. Through a swipe interface, users capture their current cravings. The recommender system turns them into candidate menus that persona agents negotiate, all visible in a chat where real users can still chime in.

The result is a complete weekly plan. The automatically generated shopping list is tailored to the chosen retailer (e.g., Coop or Migros) and cuts food waste by using what's already in stock first.

In short: MenuMingles transforms a tedious chore into an interactive experience—intelligent, sustainable and radically time‑saving.

## Repository Structure

| Directory | Description |
|-----------|-------------|
| `menu-frontend/` | Vue 3 + Vite user interface for creating and viewing menus. Includes Tailwind styling and TypeScript configuration. |
| `menu-backend/` | ASP.NET Core backend providing authentication, planning and discussion APIs. Contains `backend.csproj`, feature folders, and integration tests. |
| `menu-minglers/` | FastAPI microservice with a clean architecture. Uses Poetry for dependencies and includes health-check endpoints and tests. |
| `menu-recommender/` | FastAPI service that generates menu recommendations based on datasets and embeddings. Comes with notebooks and service modules. |
| `docs/` | Design artefacts such as diagrams and whiteboard photos. |
| `pitch/` | Slide deck used to present the project idea. |
| `screencast.mp4` | Demo of the application.

## Development

Each component is developed and tested independently. Refer to the README or documentation inside each directory for setup instructions and additional details.

## License

This repository is intended for educational purposes as part of the Bärnhäckt challenge.

