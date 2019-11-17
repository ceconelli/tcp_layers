Rails.application.routes.draw do
  resources :messages
  post "/receivemessage/:id", to: "messages#receiveFromApplicationClient"
  post "/receivemessagephy/:id", to: "messages#receiveFromPhysicalServer"
  post "/receivemessagephycli/:id", to: "messages#receiveFromPhysicalClient"
  # match '/home' => 'messages#show', :via => :get
  # For details on the DSL available within this file, see https://guides.rubyonrails.org/routing.html
end
