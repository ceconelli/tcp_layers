Rails.application.routes.draw do
  resources :messages
  post "/messagesteste/:id", to: "messages#home"
  # match '/home' => 'messages#show', :via => :get
  # For details on the DSL available within this file, see https://guides.rubyonrails.org/routing.html
end
