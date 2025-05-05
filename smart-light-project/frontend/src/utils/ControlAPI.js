export const sendControlCommand = async (mac, action) => {
    const res = await fetch("/api/control", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mac, action }),
    });
  
    if (!res.ok) {
      console.error("Failed to send control command");
    }
  };
  