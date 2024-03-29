subroutine solve(a, b, dt, begin_step, apply_H, eval_o, psi_in, n_psi, psi, psi_mid, psi_mid_next, eval_a)

    implicit none
    
    integer, intent(in) :: a, b
    real*8, intent(in) :: dt
    
    complex*16, intent(inout), dimension(n_psi) :: psi_in
    integer :: n_psi
    !f2py intent(in,out,overwrite) psi_in
    !f2py integer intent(hide), depend(psi_in) :: n_psi = len(psi_in)
    
    complex*16, intent(inout), dimension(n_psi) :: psi
    !f2py intent(in,out,overwrite) psi
    
    complex*16, intent(inout), dimension(n_psi) :: psi_mid
    !f2py intent(in,out,overwrite) psi_mid
    
    complex*16, intent(inout), dimension(n_psi) :: psi_mid_next
    !f2py intent(in,out,overwrite) psi_mid_next
    
    integer, intent(in) :: eval_a
    
    real*8 :: tol, err
    
    integer :: cont 

    external begin_step
    external apply_H
    external eval_o
    
    integer :: i
    
    tol = dt**3
    
    psi = psi_in
    
    if (eval_a .eq. 1) then
    
        call eval_o(a, psi, n_psi)
        
    end if
    
    do i = a, b - 1
    
        call begin_step(i, psi, n_psi)
    
        psi_mid = psi
        
        do while(.true.)
        
            psi_mid_next = 0d0
        
            call apply_H(i, psi_mid, psi_mid_next, n_psi)
            psi_mid_next = psi - (0d0, 1d0) * dt / 2 * psi_mid_next
        
            err = sum(abs(psi_mid_next - psi_mid))
    
            psi_mid = psi_mid_next
        
            if (err < tol) then
                exit
            end if
        
        end do
    
        psi = 2 * psi_mid - psi
            
        call eval_o(i + 1, psi, n_psi)
    
    end do
    
end subroutine solve
