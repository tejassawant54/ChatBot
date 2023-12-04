import { Client as Styletron } from 'styletron-engine-atomic';
import { Provider as StyletronProvider } from 'styletron-react';
import { DarkTheme, BaseProvider } from 'baseui';
import React, { useState, useEffect, useRef } from 'react';
import { Block } from 'baseui/block';
import { io } from 'socket.io-client';
import './App.css';
import logo from './logo.svg';
import { Input } from 'baseui/input';
import { ChevronRight } from 'baseui/icon'
import { Button } from 'baseui/button';
import { KIND as ButtonKind } from "baseui/button";
import { BACKGROUND_COLOR_TYPE, MessageCard } from "baseui/message-card";
import { DisplayXSmall, ParagraphLarge, ParagraphMedium, ParagraphSmall, ParagraphXSmall } from 'baseui/typography';
import moment from 'moment';
import { Modal, ModalBody, ModalButton, ModalFooter, ModalHeader } from 'baseui/modal';

const engine = new Styletron();


const messages = document.getElementById('messages');
const form = document.getElementById('form');
const messageInput = document.getElementById('message-input');



function App() {
  //Component Hooks
  const socket = io('http://localhost:5005');
  const messagesRef = useRef(null);
  //Component States
  const [isConnected, setIsConnected] = useState(socket.connected);
  const [messages, setMessages] = useState("");
  const [messageList, setMessageList] = useState([]);
  const [agencyID, setAgencyID] = useState("");
  const [password, setPassword] = useState("");
  const [loginModal, setLoginModal] = useState(false);

  function onConnect() {
    setIsConnected(true);
    localStorage.setItem('RASA_SESSION_ID', socket.id);
  }

  function onDisconnect() {
    setIsConnected(false);
  }

  function onResponse(value) {
    console.log("bot_uttered: ", value);
    if (value.text === "Please provide your AgencyID.") {
      setLoginModal(true);
    } else {
      let botMessage =
        <Block key={"bot/" + moment().milliseconds()} style={{ width: "100%", display: "flex", flexDirection: "row", alignItems: "center", justifyContent: "left", marginBottom: "12px" }}>
          <Block style={{ padding: "10px", backgroundColor: "#333333", borderRadius: "10px", maxWidth: "450px", minWidth: "200px", alignSelf: "flex-end" }}>
            <ParagraphLarge style={{ margin: "0px", color: "#FFFFFF", wordWrap: "break-word" }}>{value.text}</ParagraphLarge>
            <ParagraphXSmall style={{ margin: "0px", color: "#C4C4C4", wordWrap: "break-word" }}>{moment().format("LLL")}</ParagraphXSmall>
          </Block>
        </Block>;
      setMessageList(prevMessages => [...prevMessages, botMessage]);
    }
    messagesRef.current.scrollIntoView({ behavior: 'smooth' });
  }

  useEffect(() => {
    console.log("IM HERE")
    localStorage.removeItem('RASA_SESSION_ID');
    socket.on('connect', onConnect);
    socket.on('disconnect', onDisconnect);
    socket.on('bot_uttered', onResponse);

    return () => {
      socket.off('connect', onConnect);
      socket.off('disconnect', onDisconnect);
      socket.off('bot_uttered', onResponse);
    };
  }, []);

  function utter(msg) {
    console.log("uttering");
    socket.emit('user_uttered', {
      'message': msg,
      'session_id': localStorage.getItem('RASA_SESSION_ID'),
    });
  }


  async function sendMessage(event) {
    event.preventDefault();
    try {
      utter(messages);
      let userMessage =
        <Block key={"user/" + moment().milliseconds()} style={{ width: "100%", display: "flex", flexDirection: "row", alignItems: "center", justifyContent: "right", marginBottom: "12px" }}>
          <Block style={{ padding: "10px", backgroundColor: "#EDEDED", borderRadius: "10px", maxWidth: "450px", minWidth: "200px", alignSelf: "flex-end" }}>
            <ParagraphLarge style={{ margin: "0px", color: "#1B1B1B", wordWrap: "break-word" }}>{messages}</ParagraphLarge>
            <ParagraphXSmall style={{ margin: "0px", color: "#858585", wordWrap: "break-word" }}>{moment().format("LLL")}</ParagraphXSmall>
          </Block>
        </Block>
      setMessageList(prevMessages => [...prevMessages, userMessage]);
      setMessages("");
      messagesRef.current.scrollIntoView({ behavior: 'smooth' });
    }
    catch (e) {
      console.error(e);
    }
  }

  async function loginEvent() {
    try {
      await utter(`The agencyID is ${agencyID} and the password is ${password}`);
      setLoginModal(false);
    } catch (error) {
      console.error(error);
    }
  }

  return (
    <StyletronProvider value={engine}>
      <BaseProvider theme={DarkTheme}>
        <>
          <div style={{ display: "flex", flexDirection: "column", backgroundColor: "#1B1B1B", height: "100vh", }}>
            <Block style={{ display: "flex", alignItems: "center", padding: "10px", backgroundColor: "#000000", justifyContent: "space-between" }}>
              <DisplayXSmall>ChatBot Application</DisplayXSmall>
              <Block style={{ backgroundColor: "#E2E2E2", padding: "10px", display: "flex", flexDirection: "row", borderRadius: "40px", alignItems: "center" }}>
                <ParagraphMedium style={{ marginRight: "10px", marginTop: "0px", marginBottom: "0px", color: "#1B1B1B" }}>Status: </ParagraphMedium>
                <Block style={{ width: "10px", height: "10px", borderRadius: "10px", backgroundColor: isConnected ? "#03703C" : "#AB1300" }} />
              </Block>
            </Block>
            <Block style={{ flex: 1, overflowY: "auto", paddingTop: "20px", paddingLeft: "20px", paddingRight: "20px" }}>
              {
                messageList.length === 0 ?
                  <Block width="100%" height="100%" display="flex" flexDirection="column" alignItems="center" justifyContent="center">
                    <img src={logo} className="App-logo" alt="logo" />
                    <Block style={{ color: "#ffffff", fontSize: "30px", fontWeight: "bold", marginTop: "20px"}}>
                      Welcome to the ChatBot 
                    </Block>
                    <Block style={{ color: "#ffffff", fontSize: "20px", fontWeight: "bold", marginTop: "20px"}}>
                    <i>Type Message to get started</i>
                    </Block>
                  </Block> :
                  messageList.map((message) => (message))
              }
              <div style={{ height: "20px" }} ref={messagesRef} />
            </Block>
            <form onSubmit={isConnected ? sendMessage : null}>
              <Block style={{ display: "flex", alignItems: "center", padding: "10px", backgroundColor: "#000000" }}>
                <Input disabled={!isConnected} id='message' value={messages} onChange={(event) => setMessages(event.target.value)} placeholder='Type the message here' size='default' clearable />
                <Button disabled={!isConnected} size='compact' style={{ marginRight: "20px", marginLeft: "20px" }} type='submit'>
                  Send
                  <ChevronRight size={30} color='#000000' />
                </Button>
              </Block>
            </form>
          </div>
          <Modal isOpen={loginModal} onClose={() => setLoginModal(false)}>
            <ModalHeader>
              <DisplayXSmall>Enter your Credentials</DisplayXSmall>
            </ModalHeader>
            <ModalBody>
              <Input id='agencyID' value={agencyID} onChange={(event) => setAgencyID(event.target.value)} placeholder='AgencyID' size='default' clearable />
              <Block height="12px" />
              <Input type='password' value={password} onChange={(event) => setPassword(event.target.value)} placeholder='Password' size='default' />
            </ModalBody>
            <ModalFooter>
              <ModalButton kind={ButtonKind.secondary} onClick={() => setLoginModal(false)}>Cancel</ModalButton>
              <ModalButton kind={ButtonKind.primary} onClick={() => loginEvent()}>Login</ModalButton>
            </ModalFooter>
          </Modal>
        </>
      </BaseProvider>
    </StyletronProvider>
  );
}

export default App;
