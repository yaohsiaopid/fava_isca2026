- directory state: Local, Dirty, Pending, Head-Valid, List
    - `Local`: dir_S/dir_M?, if the local processor contains a cached copy of the line in either shared or exclusive state. 
    - `Dirty`: dir_M, the home thinks that there is a dirty copy of the line in the system.
    - `Pending`: dir_S_D?, current request is being processed by third node  
    - `Head.Pointer`: pointer to the remote core
- `Local’ or ‘Remote’ indicates whether the processing node is the home oft he requested memory address.
- handlers:

    - local core read request 
        - PI.Local.Get (`PI_Local_Get_Get`): local core send GetS; 
            - if home is dir_M sends Get to owner (`Head_Pointer`) and `Pending` is set
            - if home is dir_S, send back copies, `Local` is set 
    - local core write request
        - PI.Local.GetX (`PI_Local_GetX_GetX`): Local core send GetM
        
    
    - NI.Local.Get: remote core send GetS 