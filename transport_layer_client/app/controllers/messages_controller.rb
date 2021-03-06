class MessagesController < ApplicationController
  #before_action :set_message, only: [:show, :edit, :update, :destroy, :home]
  protect_from_forgery with: :null_session
  # GET /messages
  # GET /messages.json
  def index
    @messages = Message.all
  end

  # GET /messages/1
  # GET /messages/1.json
  def show
  end

  def receiveFromApplicationClient
    puts "received from application layer: " + params[:id]
    open('./../application_layer_client/messages/sent/file.txt', 'w') { |f|
      f.puts "" + params[:id]
    }
  end

  def receiveFromPhysicalServer
    require 'net/http'
    require 'uri'
    puts "received from physical server layer: " + params[:id]

    uri = URI.parse('http://localhost:8000/receive_message/')
    header = {'Content-Type': 'text/json'}
    # Create the HTTP objects
    http = Net::HTTP.new(uri.host, uri.port)
    response = Net::HTTP.post_form(uri, 'msg' => params[:id])
    puts "response: " + response.body
    open('./../physical_layer/physical/server/messages/received/transport_layer.txt', 'w') { |f|
      f.puts "" + response.body
    }
    return response.body
  end

  def receiveFromPhysicalClient
    require 'net/http'
    require 'uri'
    puts "received from physical client layer: " + params[:msg]

    uri = URI.parse('http://localhost:3000/receive_message')
    header = {'Content-Type': 'text/json'}
    # Create the HTTP objects
    http = Net::HTTP.new(uri.host, uri.port)
    response = Net::HTTP.post_form(uri, 'msg' => params[:msg])
    puts "response: " + response.body
  end
  
  # GET /messages/new
  def new
    @message = Message.new
  end

  # GET /messages/1/edit
  def edit
  end

  # POST /messages
  # POST /messages.json
  def create
    @message = Message.new(message_params)

    respond_to do |format|
      if @message.save
        format.html { redirect_to @message, notice: 'Message was successfully created.' }
        format.json { render :show, status: :created, location: @message }
      else
        format.html { render :new }
        format.json { render json: @message.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /messages/1
  # PATCH/PUT /messages/1.json
  def update
    respond_to do |format|
      if @message.update(message_params)
        format.html { redirect_to @message, notice: 'Message was successfully updated.' }
        format.json { render :show, status: :ok, location: @message }
      else
        format.html { render :edit }
        format.json { render json: @message.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /messages/1
  # DELETE /messages/1.json
  def destroy
    @message.destroy
    respond_to do |format|
      format.html { redirect_to messages_url, notice: 'Message was successfully destroyed.' }
      format.json { head :no_content }
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_message
      @message = Message.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def message_params
      params.require(:message).permit(:data)
    end
end
